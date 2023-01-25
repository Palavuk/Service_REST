# Service_IBS

This service provides simple functional, that may help data-engineers in work

# Start

## In Windows native:

Just run script start.py, for it open project directory in cmd fnd type:

       python start.py
       
This method assumes that the local machine has installed fastapi, pandas, python-multipart and "uvicorn[standard]" packages

## In docker container:

For start working just type in cmd

       docker-compose build
       docker-compose up -d
      
And go to this url in your favorite browser 

    localhost:8080/docs
