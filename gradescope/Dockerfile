FROM gradescope/auto-builds:latest

# RUN apt-get update && apt-get install -y curl dos2unix && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /autograder/source
RUN apt-get update

# ADD ./container/setup /autograder/source/setup
ADD ./container/setup.sh /autograder/source/setup.sh

# run install script
RUN /autograder/source/setup.sh
RUN apt-get install -y python3-tk
# cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# RUN apt-get update && bash /autograder/source/setup.sh && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD ./container /autograder/source
RUN cp /autograder/source/run_autograder /autograder/run_autograder

# RUN dos2unix /autograder/run_autograder /autograder/source/setup.sh

RUN chmod +x /autograder/run_autograder
