pipeline {
  agent any
  stages {

    stage('SAST: Ansible') {
      steps {
        sh 'ansible-galaxy collection install amazon.aws'
        sh 'ansible-lint ansible/'
      }
    }

    stage('SAST: Terraform + Helm') {
      steps {
        sh 'checkov -d terraform/ --framework terraform'
        sh 'checkov -d helm/rocky-target --framework helm --skip-check CKV_K8S_21,CKV_K8S_43,CKV2_K8S_6'
      }
    }

    stage('Test') {
      steps {
        sh 'helm lint helm/rocky-target'
      }
    }

    stage('Deploy') {
      steps {
        sh 'helm upgrade --install rocky helm/rocky-target --rollback-on-failure --timeout 60s'
      }
    }
  }
}
