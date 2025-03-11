pipeline{
    agent any;
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
        stage("Test"){
            steps{
                echo "Test completed"
            }
        }
        stage("Deploy"){
            steps{
                sh "docker compose up -d --build"
            }
        }
        
    }
}
