# # # # # # # # # # # # # # # #
# Run the app on Python 3.9.X #
# # # # # # # # # # # # # # # #

# # # # # # # # # # # # #
# Starting the builder  #
# # # # # # # # # # # # #

# pull official base image Python 3.9.X
FROM python:3.9-slim-buster as builder

# set the working directory
WORKDIR /usr/workspace/emp_dms

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/workspace/emp_dms/wheels -r requirements.txt


# # # # # # # # # # # # # #
# Starting the final step #
# # # # # # # # # # # # # #

# pull official base image Python 3.9.X
FROM python:3.9-slim-buster

# create dierctory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app


# create the appropiate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/employee_dms
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/workspace/emp_dms/wheels /wheels
COPY --from=builder /usr/workspace/emp_dms/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

RUN chown -R app:app $APP_HOME

USER app