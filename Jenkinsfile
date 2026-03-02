pipeline {
  agent {
    docker { image 'python:3.11-slim' }
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Install') {
      steps {
        sh '''
          python -V
          pip install -U pip
          pip install -r requirements-dev.txt
        '''
      }
    }

    stage('Tests') {
      steps {
        sh 'pytest -q'
      }
    }
  }
}
