# CT-213-Exam-DTTS
This project was made as part of the final exam of the CT-213 (Artificial intelligence for mobile robotics) of the ITA
Creation of an agent that learns to play Don't Touch The Spikes using imitation learning
The base game record in a .csv file every 1/60 second the actual x and y position, the previous(1/60 second before) x and y position - so that the agent can know the velocitys at which the bird is going - the position of the spikes and the decision of the player, 1 for jump and 0 for nothing.
The agent is trained with a Supervised Learning neural network.
 
A implementação tem os seguintes arquivos: três .pngs que são usados no jogo, um arquivo data.csv que é usado para armazenar os dados utilizados para o treinamento da rede neural, o score.txt que guarda todos os scores alcançados pelo jogador ou pelo agente, uma pasta my_model contendo um modelo de rede neural já treinado, a main.py que contém o código central da implementação, a simulation.py que contém tudo da simulação do jogo usando a biblioteca pygame e por último o arquivo imitation_learning.py que é usada para treinar a rede neural e armazená-la na pasta my_model.
Antes de utilizar o código no arquivo simulation.py existem duas linhas que podem ser mudadas conforme seja neccessário, uma que guarda a informação se o agente está jogando e outra se deve-se salvar o estado a cada frame, é interessante mudar a primeira linha caso você queira jogar no lugar do agente, por exemplo para captar dados para treinar a rede neural, e a segunda caso você esteja rodando algum teste e não quer que sejam gravados dados que não condizem com um jogador real.
Para treinar a rede neural basta adicionar um arquivo data.csv na pasta do código e rodar o arquivo imitation_learning.py que ele irá treinar a rede sendo que a partir da linha 35 é possível alterar o formato da rede neural.
Por último, para rodar o código seja para jogar ou para ver o agente jogando basta rodar a main.py.
