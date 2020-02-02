# Run in bg
kill $(ps aux | grep '[v]aasu.py' | awk '{print $2}')
nohup python3 vaasu.py &> run.log &