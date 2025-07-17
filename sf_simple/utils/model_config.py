"""
Model Configuration System for Script Fury Simple
Allows easy switching between different AI models for different tasks
"""

import os
from typing import Dict, Optional

class ModelConfig:
    """Configuration for AI models used in different tasks"""
    
    def __init__(self):
        self.models = {
            # Complex analysis tasks - use best available model
            'screenplay_analysis': os.getenv('SCREENPLAY_MODEL', 'gpt-4o'),
            'character_extraction': os.getenv('CHARACTER_MODEL', 'gpt-4o'),
            'scene_analysis': os.getenv('SCENE_MODEL', 'gpt-4o'),
            
            # Fast processing tasks - use fast models
            'prompt_sanitization': os.getenv('SANITIZATION_MODEL', 'o3-mini'),
            'basic_info_extraction': os.getenv('INFO_MODEL', 'gpt-4o'),
            
            # Image generation - use image-specific model
            'image_generation': os.getenv('IMAGE_MODEL', 'gpt-image-1'),
            
            # Fallback model for any task
            'fallback': os.getenv('FALLBACK_MODEL', 'gpt-4o-mini')
        }
        
        # Model capabilities and costs
        self.model_info = {
            'gpt-4o': {
                'type': 'premium',
                'speed': 'medium',
                'quality': 'highest',
                'cost': 'high',
                'best_for': ['complex_analysis', 'character_extraction', 'scene_analysis']
            },
            'o3-mini': {
                'type': 'fast',
                'speed': 'very_fast',
                'quality': 'good',
                'cost': 'low',
                'best_for': ['prompt_sanitization', 'quick_tasks']
            },
            'gpt-4o-mini': {
                'type': 'balanced',
                'speed': 'fast',
                'quality': 'good',
                'cost': 'medium',
                'best_for': ['general_tasks', 'fallback']
            },
            'gpt-image-1': {
                'type': 'specialized',
                'speed': 'medium',
                'quality': 'high',
                'cost': 'medium',
                'best_for': ['image_generation']
            }
        }
    
    def get_model(self, task: str) -> str:
        """Get the configured model for a specific task"""
        return self.models.get(task, self.models['fallback'])
    
    def get_model_info(self, model: str) -> Dict:
        """Get information about a specific model"""
        return self.model_info.get(model, {})
    
    def set_model(self, task: str, model: str) -> None:
        """Set the model for a specific task"""
        self.models[task] = model
    
    def use_premium_models(self) -> None:
        """Configure to use premium models for best quality"""
        self.models.update({
            'screenplay_analysis': 'gpt-4o',
            'character_extraction': 'gpt-4o',
            'scene_analysis': 'gpt-4o',
            'prompt_sanitization': 'gpt-4o',
            'basic_info_extraction': 'gpt-4o'
        })
        print("🚀 Premium models enabled for maximum quality")
    
    def use_fast_models(self) -> None:
        """Configure to use fast models for speed"""
        self.models.update({
            'screenplay_analysis': 'o3-mini',
            'character_extraction': 'o3-mini',
            'scene_analysis': 'o3-mini',
            'prompt_sanitization': 'o3-mini',
            'basic_info_extraction': 'o3-mini'
        })
        print("⚡ Fast models enabled for maximum speed")
    
    def use_balanced_models(self) -> None:
        """Configure to use balanced models for good speed/quality"""
        self.models.update({
            'screenplay_analysis': 'gpt-4o',
            'character_extraction': 'gpt-4o',
            'scene_analysis': 'gpt-4o',
            'prompt_sanitization': 'o3-mini',
            'basic_info_extraction': 'gpt-4o-mini'
        })
        print("⚖️ Balanced models enabled for optimal speed/quality")
    
    def print_config(self) -> None:
        """Print current model configuration"""
        print("\n🤖 Current Model Configuration:")
        print("=" * 50)
        for task, model in self.models.items():
            info = self.get_model_info(model)
            quality = info.get('quality', 'unknown')
            speed = info.get('speed', 'unknown')
            cost = info.get('cost', 'unknown')
            print(f"  {task}: {model} (Quality: {quality}, Speed: {speed}, Cost: {cost})")
        print("=" * 50)

# Global model configuration instance
model_config = ModelConfig()

def get_model_for_task(task: str) -> str:
    """Get the configured model for a specific task"""
    return model_config.get_model(task)

def configure_models(mode: str = 'balanced') -> None:
    """Configure models for a specific mode"""
    if mode == 'premium':
        model_config.use_premium_models()
    elif mode == 'fast':
        model_config.use_fast_models()
    elif mode == 'balanced':
        model_config.use_balanced_models()
    else:
        print(f"Unknown mode: {mode}. Using balanced configuration.")
        model_config.use_balanced_models()

def print_model_config() -> None:
    """Print current model configuration"""
    model_config.print_config()

# Set default configuration based on environment
default_mode = os.getenv('MODEL_MODE', 'balanced')
configure_models(default_mode)