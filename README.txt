PRE REQUIREMENTS:

- This project is designed and structured to work from WSL/Linux.

- Install Docker

- Install Poetry
|
|- with the `pip install poetry` command from the WSL console.


##Instructions:

1. From the console, navigate to the file path.

2. Run the 'docker ps' command to verify that there are no services running in Docker.

3. Run the 'make up-all' command to raise the project containers.

4. From the console, go to the path 'infra/arangobd/migration> make migration' to install the database.

5. From the console, run 'docker ps' to verify if the 4 corresponding services are running.

6. From the browser, open the port 'localhost:9000/' where the project UI will open.
|
- In the upper left corner you can select the model you prefer, whether it is a base model or the improved one.

7. Load the fields corresponding to your product.

8. If you want to access the database, you can access it from 'http://localhost:8529/_db/_system/_admin/aardvark/index.html#login' and using the password stored in the
infra/arangobd/docker-compose.yml

9. After the test run, you must download the containers with the 'make all-down' command.
