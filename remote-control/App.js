import React, { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';

export default function App() {
  const [direction, setDirection] = useState('');

  const sendPostRequest = async () => {
    try {
      const response = await fetch('http://192.168.119.176:5000/robot-control', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ direction }),
      });

      const data = await response.json();
      console.log('Response:', data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.buttonRow}>
        <TouchableOpacity style={styles.button} onPress={() => { setDirection('w'); sendPostRequest(); }}>
          <Text style={styles.buttonText}>İleri</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.buttonRow}>
        <TouchableOpacity style={styles.button} onPress={() => { setDirection('a'); sendPostRequest(); }}>
          <Text style={styles.buttonText}>Sol</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.button} onPress={() => { setDirection('s'); sendPostRequest(); }}>
          <Text style={styles.buttonText}>Geri</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.button} onPress={() => { setDirection('d'); sendPostRequest(); }}>
          <Text style={styles.buttonText}>Sağ</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.buttonRow}>
        <TouchableOpacity style={styles.emergencyButton} onPress={() => { setDirection('x'); sendPostRequest(); }}>
          <Text style={styles.buttonText}>Acil Stop</Text>
        </TouchableOpacity>
      </View>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonRow: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#4CAF50',
    padding: 20,
    margin: 10,
    borderRadius: 10,
    width: 100,  // Buton genişliği
    alignItems: 'center',
    justifyContent: 'center',
  },
  emergencyButton: {
    backgroundColor: 'red',
    padding: 20,
    margin: 10,
    borderRadius: 10,
    width: 200,  // Acil Stop butonu genişliği
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
