# OptoTransportAnalysis
Data analysis infrastructure for work in Xu lab @ UW across optical and transport measurements.\

Instructions for installing OptoTransport conda environment:\
This repository contains an environment.yml file, which directs Conda 
to establish an environment with all necessary packages to make this
library work. You can install the environment using the following steps: \
    1. Step into the directory where the environment.yml file is stored. \
    2. Create the environment using the line $ conda env create -f environment.yml \
    3. Activate the environment using $ conda activate OptoTransport \
More info:
    * Installing conda: https://learning.anaconda.cloud/?utm_campaign=starter-mktg&utm_medium=online-advertising&utm_source=google&gclid=CjwKCAiA-dCcBhBQEiwAeWidtVqZ-CXpReEyQC5J6LUkmnVll_6RWkciK_s15SbfN0mTBgxQ5lMuPRoCn3AQAvD_BwE \
    * Activating environments using .yml files: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html \
For updating conda environment:
    1. Update environment.yml file with desired packages \
    2. Activate the environment and step into the directory where environment.yml is stored \
    3. Update the environment using $ conda env update --file environment.yml --prune \
For faster performance, install mamba and run the above command using $ mamba instead of $ conda