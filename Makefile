deps:
	curl -O "http://download.hazelcast.com/download.jsp?version=hazelcast-3.4&type=tar&p=8958592"

# this assumes you're using pyenv and have placed the Hazelcast jars under lib
run:
	export CLASSPATH=$CLASSPATH:lib/hazelcast-3.4.jar python main.py
