from imp import reload
import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        reload=True
    )