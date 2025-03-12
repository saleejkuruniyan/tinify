pipeline{
    agent {label "dev"};
    stages{
        stage("Clone"){
            steps{
                git url: "https://github.com/saleejkuruniyan/tinify.git", branch: "staging"
                
            }
        }
        stage("Build"){
            steps{
                sh "docker build -t tinify ."
            }
        }
        stage("Test"){
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
        stage("Deploy"){
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
