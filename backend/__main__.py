import uvicorn

def main():
    uvicorn.run(app='backend.app:app', host='127.0.0.1', port=4200, reload=True)

if __name__ == '__main__':
    main()