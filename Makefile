#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = GP-sensorData
PYTHON_INTERPRETER = python3
SHELL=/bin/bash

ifeq (,$(shell which conda))
	HAS_CONDA=False
else
	HAS_CONDA=True
endif


#################################################################################
# COMMANDS                                                                      #
#################################################################################

update: 
	conda env update --name $(PROJECT_NAME) --file environment.yml --prune

## Set up python interpreter environment
environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda env create -n $(PROJECT_NAME) -f environment.yml
else
	conda create --name $(PROJECT_NAME) python=2.7
endif
		@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	@pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already intalled.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## Remove env and all dependencies
remove_environment:
	conda remove --name $(PROJECT_NAME) --all
