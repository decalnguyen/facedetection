package main

import (
	"encoding/json"
	"fmt"
	"log"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

const (
	mqttBroker = "192.168.120.88:1883"
	topicPub   = "door/status"
	topicSub   = "door/resquest"
	user       = "mmtt21-2"
	pass       = "mmtt212ttmm"
	qos        = 0
)

func sub(client mqtt.Client, topic string, qos byte) {
	if stt := client.Connect(); stt.Wait() && stt.Error() != nil {
		log.Println("Error connecting to MQTT broker: ", stt.Error())
	} else {
		log.Println("Server connected successfully to MQTT Broker: ", client.IsConnected())
	}

	stt := client.Subscribe(topicSub, qos, messagePubHandler)
	stt.Wait()
	log.Println("Successful subcribing to MQTT Topic")
}

func pub(client mqtt.Client, topic string, qos byte, sendPayload string) {
	if stt := client.Connect(); stt.Wait() && stt.Error() != nil {
		log.Println("Error connecting to MQTT broker: ", stt.Error())
	} else {
		log.Println("Device connected successfully to MQTT Broker: ", client.IsConnected())
	}

	encodedMes, err := json.Marshal(sendPayload)

	fmt.Println("Marshal error", err)

	stt := client.Publish(topicPub, qos, false, encodedMes)
	stt.Wait()
	time.Sleep(time.Second)
	log.Println("Successful publishing to MQTT Topic ")
}

func HandleMessageSensor(client mqtt.Client, message mqtt.Message) {
	data := string(message.Payload())

	if data == "OPEN" {
		//client.Publish(topicPub, 0, false, []byte("OPEN"))
		pub(client, topicPub, 0, []byte("OPEN"))
	}
}
func reconnect() {}

var (
	connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
		log.Println("Connected")
	}
)

var (
	connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
		log.Println("Lost Connect: ", err)
	}
)
var (
	messagePubHandler mqtt.MessageHandler = func(client mqtt.Client, message mqtt.Message) {
		//var decodedMess Device
		HandleMessageSensor(client, message)
	}
)

func main() {

	opts := mqtt.NewClientOptions()
	opts.AddBroker(mqttBroker)
	opts.SetUsername(user)
	opts.SetPassword(pass)
	opts.SetDefaultPublishHandler(messagePubHandler)
	opts.OnConnect = connectHandler
	opts.OnConnectionLost = connectLostHandler
	client := mqtt.NewClient(opts)

	sub(client, topicSub, qos)
	for {
		time.Sleep(1 * time.Second)
	}
	//pub(client, topicPub, qos, "RED")

}
