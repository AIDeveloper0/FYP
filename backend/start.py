import uvicorn
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("🚀 Starting Mermaid Generator API (New Approach)")
    logger.info("📝 No AI models - using rule-based generation")
    logger.info("🔗 API will be available at: http://localhost:8000")
    logger.info("📚 Documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )