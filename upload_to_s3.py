#!/usr/bin/env python3
"""
S3上传脚本 - 用于将生成的视频上传到S3并更新DynamoDB
"""

import boto3
import os
import sys
from pathlib import Path

def upload_video_to_s3(task_uuid, scene_type):
    """上传视频到S3并更新DynamoDB"""
    
    # S3配置
    s3_client = boto3.client('s3', region_name='us-east-1')
    s3_bucket = 'documents-distrubution'
    s3_folder = 'cosmos-video'
    cloudfront_domain = 'd3bb5kiveg9mt4.cloudfront.net'
    
    # DynamoDB配置
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('SceneGeneration')
    
    # 确定文件名
    if scene_type == 'SingleView':
        local_video = f"{task_uuid}.mp4"
    else:  # MultiView
        local_video = f"{task_uuid}_grid.mp4"
    
    local_path = f"/home/ubuntu/cosmos-predict1/{local_video}"
    s3_key = f"{s3_folder}/{local_video}"
    
    try:
        # 检查本地文件是否存在
        if not os.path.exists(local_path):
            print(f"❌ Video file not found: {local_path}")
            return False
        
        print(f"📁 Found video file: {local_path}")
        file_size = os.path.getsize(local_path) / (1024 * 1024)  # MB
        print(f"📊 File size: {file_size:.2f} MB")
        
        # 上传到S3
        print(f"⬆️  Uploading to s3://{s3_bucket}/{s3_key}")
        s3_client.upload_file(
            local_path,
            s3_bucket,
            s3_key,
            ExtraArgs={'ContentType': 'video/mp4'}
        )
        
        # 生成CloudFront URL
        video_url = f"{cloudfront_domain}/{s3_key}"
        print(f"🌐 CloudFront URL: https://{video_url}")
        
        # 更新DynamoDB
        print(f"💾 Updating DynamoDB for task {task_uuid}")
        table.update_item(
            Key={'uuid': task_uuid},
            UpdateExpression='SET video_link = :url',
            ExpressionAttributeValues={':url': video_url}
        )
        
        print(f"✅ Successfully uploaded and updated video_link for {task_uuid}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 upload_to_s3.py <uuid> <scene_type>")
        print("Example: python3 upload_to_s3.py 5a793b2f-4c9d-480b-8606-2c7f26c1234 MultiView")
        sys.exit(1)
    
    task_uuid = sys.argv[1]
    scene_type = sys.argv[2]
    
    if scene_type not in ['SingleView', 'MultiView']:
        print("❌ scene_type must be 'SingleView' or 'MultiView'")
        sys.exit(1)
    
    print(f"🚀 Starting upload for {scene_type} task: {task_uuid}")
    success = upload_video_to_s3(task_uuid, scene_type)
    
    if success:
        print("🎉 Upload completed successfully!")
        sys.exit(0)
    else:
        print("💥 Upload failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
