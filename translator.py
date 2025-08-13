import boto3
import json
import logging
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class BedrockTranslator:
    def __init__(self, region_name='us-east-1'):
        """初始化Bedrock翻译器"""
        self.bedrock = boto3.client('bedrock-runtime', region_name=region_name)
        self.model_id = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'
    
    def translate_to_english(self, chinese_text: str, max_retries: int = 5) -> Optional[str]:
        """
        使用Claude翻译中文文本为英文，带重试机制
        
        Args:
            chinese_text: 需要翻译的中文文本
            max_retries: 最大重试次数
            
        Returns:
            翻译后的英文文本，如果翻译失败返回None
        """
        if not chinese_text or not chinese_text.strip():
            return chinese_text
        
        # 检查是否已经是英文（简单检测）
        if self._is_likely_english(chinese_text):
            logger.info(f"Text appears to be English already: {chinese_text[:50]}...")
            return chinese_text
        
        prompt = f"""Please translate the following Chinese text to English, following these requirements:
1. Keep the translation natural and descriptive, suitable for AI video generation
2. Return the translation as a SINGLE PARAGRAPH without line breaks
3. The translation should be CONCISE and NO MORE THAN 300 WORDS
4. Only return the English translation without any additional explanation

Chinese text: {chinese_text}"""

        for attempt in range(max_retries + 1):
            try:
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
                
                response = self.bedrock.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(body)
                )
                
                response_body = json.loads(response['body'].read())
                english_text = response_body['content'][0]['text'].strip()
                
                # 移除所有换行符，确保是单个段落
                english_text = ' '.join(english_text.split())
                
                # 记录翻译结果的字数
                word_count = len(english_text.split())
                logger.info(f"Translation word count: {word_count}")
                
                logger.info(f"Translation successful: {chinese_text[:30]}... -> {english_text[:30]}...")
                return english_text
                
            except Exception as e:
                error_msg = str(e)
                if "ThrottlingException" in error_msg or "Too many requests" in error_msg:
                    if attempt < max_retries:
                        wait_time = (attempt + 1) * 5  # 递增等待时间：5s, 10s, 15s
                        logger.warning(f"Rate limited, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"Translation failed after {max_retries} retries due to rate limiting")
                        return None
                else:
                    logger.error(f"Translation failed for text: {chinese_text[:50]}... Error: {error_msg}")
                    return None
        
        return None
    
    def _is_likely_english(self, text: str) -> bool:
        """简单检测文本是否可能是英文"""
        # 计算ASCII字符比例
        ascii_chars = sum(1 for c in text if ord(c) < 128)
        total_chars = len(text)
        
        if total_chars == 0:
            return True
            
        ascii_ratio = ascii_chars / total_chars
        # 如果ASCII字符占比超过80%，认为可能是英文
        return ascii_ratio > 0.8
