# Building the Toolset

Make sure you have Docker Installed with latest versions.


## Build Docker Container for consistent env

From the root of the project run:

`docker-compose build`

If all goes well the container and service should build without error

## Bash Alias
Add the following alias to you ~/bash_profile

`alias p2v="docker-compose run --rm prayer2vec"`




