#!/usr/bin/env python3
import os
import sys
from loguru import logger
from config import settings
from utils.logging import setup_logging
from core.agent import VoiceAgent
from tools.web_search import search_web
from tools.email_handler import send_email
from tools.calendar_integration import get_calendar_events, create_event
from tools.weather_api import get_weather
from tools.task_manager import add_task, list_tasks, complete_task

def setup_agent() -> VoiceAgent:
    setup_logging()
    logger.info("Starting AI Voice Agent")
    
    try:
        agent = VoiceAgent(llm_provider="openai")
    except ValueError:
        logger.warning("OpenAI not available, trying Anthropic...")
        try:
            agent = VoiceAgent(llm_provider="anthropic")
        except ValueError:
            logger.error("No LLM providers available")
            sys.exit(1)
    
    logger.info("Registering tools...")
    
    agent.register_tool(name="search_web", func=search_web, description="Search the web for information", parameters={"query": {"type": "string"}, "num_results": {"type": "integer"}})
    agent.register_tool(name="get_weather", func=get_weather, description="Get current weather for a city", parameters={"city": {"type": "string"}})
    agent.register_tool(name="get_calendar_events", func=get_calendar_events, description="Get upcoming calendar events", parameters={"days_ahead": {"type": "integer"}})
    agent.register_tool(name="create_event", func=create_event, description="Create a new calendar event", parameters={"title": {"type": "string"}, "date": {"type": "string"}, "time": {"type": "string"}})
    agent.register_tool(name="send_email", func=send_email, description="Send an email", parameters={"recipient": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}})
    agent.register_tool(name="add_task", func=add_task, description="Add a new task", parameters={"title": {"type": "string"}, "priority": {"type": "string"}, "due_date": {"type": "string"}})
    agent.register_tool(name="list_tasks", func=list_tasks, description="List all tasks", parameters={"priority": {"type": "string"}, "completed": {"type": "boolean"}})
    agent.register_tool(name="complete_task", func=complete_task, description="Mark a task as complete", parameters={"task_id": {"type": "integer"}})
    
    logger.info("Agent setup complete")
    return agent

def main():
    try:
        agent = setup_agent()
        
        logger.info("\n=== Example 1: Single Command ===")
        response = agent.process_voice_command(voice_input="What's the weather like in New York?")
        logger.info(f"Agent response: {response}")
        
        logger.info("\n=== Example 2: Task Management ===")
        response = agent.process_voice_command(voice_input="Add a task to call the doctor")
        logger.info(f"Agent response: {response}")
        
        logger.info("\n=== Example 3: Interactive Session ===")
        logger.info("Uncomment the line below to start interactive voice session")
        
    except KeyboardInterrupt:
        logger.info("Application interrupted")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
