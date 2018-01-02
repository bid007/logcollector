
## Installation steps for Linux Machines
    # Download the Source folder
    # Change the directory to Source from commandline
    # Install rabbitmq
        * sudo apt-get update && sudo apt-get install rabbitmq-server
        * or for unix brew install rabbitmq
        * start rabbitmq ( brew services start rabbitmq for unix)
        * for linux (service rabbitmq-server start)
    # Install PostgreSQL 
    # Go to Source directory from commandline
    # psql -U postgres < schema.sql 
    # Make sure you are using python3
    # pip install -r pip.txt
    # Go to src inside of Source from commandline
    # Run Unit test using : python -m unittest discover test    
    # Inside configs change emailconfig.ini for smtp server (no spaces between =)
    # Inside xml input the clients using the same format
    # Make sure clients are using python3 and have pycrypto installed
    # Now change current directory to src 
    # Run 3 celery instances 
        * celery -A tasks worker -Q log --loglevel=info
        * celery -A tasks worker -Q email --loglevel=info
        * celery -A tasks worker -Q ssh --loglevel=info
    # python main.py -t 1 -n 5 -cli xml/clients.xml -econf configs/emailconfig.ini 
        * -t for time interval (like here the script will run for 5 times in 1 sec interval)
        * -n for number of times to run ( -n 0 means run forever)
        * -cli needs the clients file which should  be inside xml
        * -econf needs the emailconfig which should be inside configs
    # Running the above command would  send email if matches found, also save the log in         database

## Requirements not complete
    * Testcases are not writtent for every thing
    * Works with only linux Machines
    * But can be extended

# Issues and other ideas
    * Writing test case for network applications is dificult
    * Classes and functions can be modify to work on single responsibility principle
    * Classes and functions could have been more open to extension 
    