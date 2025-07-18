"""
AI-based prompt sanitization system for storyboard generation.
Pure, side-effect-free approach using AI moderation.
"""

import os
import asyncio
from typing import Tuple, List, Dict, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv
from .model_config import get_model_for_task

load_dotenv()


class AIPromptSanitizer:
    """Pure AI-based prompt sanitizer that uses OpenAI to moderate and clean prompts."""

    def __init__(self) -> None:
        self.client = None

    def _get_client(self) -> AsyncOpenAI:
        """Get OpenAI client for moderation."""
        if self.client is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            self.client = AsyncOpenAI(api_key=api_key)
        return self.client

    async def ai_sanitize_prompt(self, prompt: str) -> Tuple[str, List[str], bool]:
        """
        Use AI to sanitize and improve prompt for storyboard generation.
        
        Args:
            prompt: Original prompt text
            
        Returns:
            Tuple of (sanitized_prompt, changes_made, is_sensitive_content)
        """
        try:
            client = self._get_client()
            
            # Step 1: AI moderation check
            moderation_response = await client.moderations.create(input=prompt)
            is_flagged = moderation_response.results[0].flagged
            
            # Step 2: AI-powered prompt cleaning and enhancement using configured model
            sanitization_response = await client.chat.completions.create(
                model=get_model_for_task('prompt_sanitization'),
                messages=[
                    {
                        "role": "system",
                        "content": """You are a professional storyboard prompt specialist. Your job is to take screenplay-based prompts and make them perfect for AI image generation while maintaining artistic integrity.

TASK: Rewrite the prompt to be:
1. Safe for AI image generation (no violence, adult content, etc.)
2. Focused on professional storyboard aesthetics 
3. Cinematically precise and clear
4. Suitable for black & white line art

GUIDELINES:
- Replace violent terms with cinematic alternatives (e.g., "gunfight" → "tense confrontation")
- Make mature content artistic and tasteful (e.g., "nude" → "artistic figure study")
- Add professional storyboard context
- Keep the core visual story intact
- Use film/art terminology
- Focus on composition, emotion, and storytelling

Return a JSON object with:
- "sanitized_prompt": The cleaned, enhanced prompt
- "changes_made": Array of specific changes made
- "is_sensitive": Boolean if original contained sensitive content
- "confidence": 1-10 rating of how well the story intent is preserved"""
                    },
                    {
                        "role": "user",
                        "content": f"Please sanitize and enhance this storyboard prompt:\n\n{prompt}"
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(sanitization_response.choices[0].message.content)
            
            sanitized_prompt = result.get('sanitized_prompt', prompt)
            changes_made = result.get('changes_made', [])
            is_sensitive = result.get('is_sensitive', False) or is_flagged
            
            # Step 3: Add professional storyboard context
            final_prompt = self._add_storyboard_context(sanitized_prompt, is_sensitive)
            
            return final_prompt, changes_made, is_sensitive
            
        except Exception as e:
            print(f"❌ AI sanitization failed: {e}")
            # Fallback: Just add basic context
            safe_prompt = self._add_storyboard_context(prompt, False)
            return safe_prompt, ["Used fallback sanitization"], False

    def _add_storyboard_context(self, prompt: str, is_sensitive: bool = False) -> str:
        """Add professional storyboard context to prompt."""
        if is_sensitive:
            prefix = (
                "Professional film storyboard illustration, black and white line art style. "
                "Artistic and tasteful approach suitable for serious dramatic production. "
                "Focus on emotional storytelling and cinematic composition. "
            )
            suffix = (
                " Render as sophisticated storyboard art with classical artistic restraint. "
                "Emphasize narrative and emotional content over graphic details."
            )
        else:
            prefix = (
                "Professional storyboard illustration, black and white line art style. "
                "Clean vector-like lines, minimal detail, focus on clear action and composition. "
            )
            suffix = (
                " Animation studio storyboard quality, broadcast standard, "
                "professional film production storyboard."
            )
        
        return prefix + prompt + suffix

    def sanitize_prompt_sync(self, prompt: str) -> Tuple[str, List[str], bool]:
        """Synchronous wrapper for AI sanitization with proper cleanup."""
        try:
            # Check if we're already in an event loop
            try:
                loop = asyncio.get_running_loop()
                # If we're in a loop, use basic sanitization to avoid conflicts
                safe_prompt = self._add_storyboard_context(prompt, False)
                return safe_prompt, ["Used basic sanitization (async conflict avoided)"], False
            except RuntimeError:
                # No running loop, safe to create new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    result = loop.run_until_complete(self.ai_sanitize_prompt(prompt))
                    return result
                finally:
                    # CRITICAL: Close client connections before closing event loop
                    if self.client:
                        try:
                            loop.run_until_complete(self.client.close())
                            self.client = None  # Reset client after cleanup
                        except Exception as e:
                            print(f"⚠️ Client cleanup warning: {e}")
                    
                    # Always cleanup event loop
                    loop.close()
                    
        except Exception as e:
            print(f"❌ Sync sanitization failed: {e}")
            # Fallback: Basic context addition
            safe_prompt = self._add_storyboard_context(prompt, False)
            return safe_prompt, ["Used basic fallback"], False

    async def batch_sanitize_prompts(self, prompts: List[str]) -> List[Tuple[str, List[str], bool]]:
        """Sanitize multiple prompts efficiently."""
        results = []
        
        for prompt in prompts:
            result = await self.ai_sanitize_prompt(prompt)
            results.append(result)
            
        return results

    def is_sanitization_enabled(self) -> bool:
        """Check if AI sanitization is enabled."""
        return os.getenv('USE_AI_PROMPT_SANITIZATION', 'true').lower() == 'true'


# Global sanitizer instance
_sanitizer_instance = None


def get_ai_prompt_sanitizer() -> AIPromptSanitizer:
    """Get the global AI prompt sanitizer instance."""
    global _sanitizer_instance
    if _sanitizer_instance is None:
        _sanitizer_instance = AIPromptSanitizer()
        print("🤖 Initialized AI-based prompt sanitizer (pure, side-effect-free)")
    return _sanitizer_instance


def sanitize_prompt_for_storyboard(prompt: str) -> Tuple[str, List[str], bool]:
    """
    Sanitize a prompt for storyboard generation using pure AI moderation.
    
    Args:
        prompt: Original prompt text
        
    Returns:
        Tuple of (sanitized_prompt, changes_made, is_sensitive_content)
    """
    sanitizer = get_ai_prompt_sanitizer()
    
    if sanitizer.is_sanitization_enabled():
        return sanitizer.sanitize_prompt_sync(prompt)
    else:
        # Just add basic storyboard context
        enhanced_prompt = sanitizer._add_storyboard_context(prompt, False)
        return enhanced_prompt, ["Added storyboard context only"], False