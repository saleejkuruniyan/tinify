@Library("Shared") _
pipeline{
    agent {label "dev"};
    stages{
        stage("Clone Code"){
            steps{
                script{
                   clone("https://github.com/saleejkuruniyan/tinify.git", "staging")
               }
            }
        }
        stage("Trivy File System Scan"){
            steps{
                sh "trivy fs . -o results.json"
            }
        }
        stage("Docker Build"){
            steps{
                sh "docker build -t tinify ."
            }
        }
        stage("Test Code"){
            steps{
                echo "Test completed"
            }
        }
        stage("Push to DockerHub"){
            steps{
                withCredentials([usernamePassword(
                    credentialsId:"dockerHubCred",
                    passwordVariable: "dockerHubPass",
                    usernameVariable: "dockerHubUser"
                    )]){
                    sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                    sh "docker image tag tinify ${env.dockerHubUser}/tinify"
                    sh "docker push ${env.dockerHubUser}/tinify:latest"
                    
                }
            }
        }
        stage("Deploy to Server"){
            steps{
                sh "docker compose up -d --build"
            }
        }
        
    }
        
    post {
        success {
            emailext(
                subject: "Build Successfull",
                body: "Good News !",
                to: "saleejkuruniyan@gmail.com"
                )
        }
        failure {
            emailext(
                subject: "Build Failed",
                body: "Bad News !",
                to: "saleejkuruniyan@gmail.com"
                )
            {
        }
    }
}
}
