import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, Alert } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { authAPI } from '../utils/api';
import { storage } from '../utils/storage';

const TAMIL_NADU_DISTRICTS = [
    'Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri',
    'Dindigul', 'Erode', 'Kallakurichi', 'Kanchipuram', 'Kanyakumari', 'Karur',
    'Krishnagiri', 'Madurai', 'Nagapattinam', 'Namakkal', 'Salem', 'Thanjavur',
    'Tiruchirappalli', 'Tirunelveli', 'Tiruppur', 'Vellore', 'Virudhunagar'
];

const RegisterScreen = ({ navigation }) => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        password: '',
        district: '',
    });
    const [loading, setLoading] = useState(false);

    const handleRegister = async () => {
        if (!formData.name || !formData.password || !formData.district) {
            Alert.alert('Error', 'Please fill in all required fields');
            return;
        }

        setLoading(true);
        try {
            const response = await authAPI.register(formData);
            await storage.setItem('user', response.data);
            navigation.replace('FarmerForm');
        } catch (error) {
            Alert.alert('Registration Failed', error.response?.data?.error || 'Registration failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <ScrollView contentContainerStyle={styles.container}>
            <View style={styles.card}>
                <Text style={styles.title}>Register / பதிவு செய்ய</Text>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Name / பெயர் *</Text>
                    <TextInput
                        style={styles.input}
                        value={formData.name}
                        onChangeText={(text) => setFormData({ ...formData, name: text })}
                        placeholder="Enter your name"
                    />
                </View>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Email / மின்னஞ்சல்</Text>
                    <TextInput
                        style={styles.input}
                        value={formData.email}
                        onChangeText={(text) => setFormData({ ...formData, email: text })}
                        placeholder="farmer@example.com"
                        keyboardType="email-address"
                        autoCapitalize="none"
                    />
                </View>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Phone / தொலைபேசி</Text>
                    <TextInput
                        style={styles.input}
                        value={formData.phone}
                        onChangeText={(text) => setFormData({ ...formData, phone: text })}
                        placeholder="9876543210"
                        keyboardType="phone-pad"
                    />
                </View>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>District / மாவட்டம் *</Text>
                    <View style={styles.pickerContainer}>
                        <Picker
                            selectedValue={formData.district}
                            onValueChange={(value) => setFormData({ ...formData, district: value })}
                        >
                            <Picker.Item label="Select District" value="" />
                            {TAMIL_NADU_DISTRICTS.map(district => (
                                <Picker.Item key={district} label={district} value={district} />
                            ))}
                        </Picker>
                    </View>
                </View>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Password / கடவுச்சொல் *</Text>
                    <TextInput
                        style={styles.input}
                        value={formData.password}
                        onChangeText={(text) => setFormData({ ...formData, password: text })}
                        placeholder="••••••••"
                        secureTextEntry
                    />
                </View>

                <TouchableOpacity
                    style={[styles.button, loading && styles.buttonDisabled]}
                    onPress={handleRegister}
                    disabled={loading}
                >
                    <Text style={styles.buttonText}>
                        {loading ? 'Loading...' : 'Register / பதிவு செய்ய'}
                    </Text>
                </TouchableOpacity>

                <TouchableOpacity onPress={() => navigation.goBack()}>
                    <Text style={styles.linkText}>
                        Already have an account? Login / உள்நுழைய
                    </Text>
                </TouchableOpacity>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flexGrow: 1,
        padding: 20,
        backgroundColor: '#f0fdf4',
    },
    card: {
        backgroundColor: 'white',
        borderRadius: 20,
        padding: 24,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 8,
        elevation: 5,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#15803d',
        textAlign: 'center',
        marginBottom: 24,
    },
    inputContainer: {
        marginBottom: 16,
    },
    label: {
        fontSize: 16,
        fontWeight: '600',
        color: '#333',
        marginBottom: 8,
    },
    input: {
        borderWidth: 2,
        borderColor: '#d1d5db',
        borderRadius: 12,
        padding: 16,
        fontSize: 16,
        backgroundColor: '#fff',
    },
    pickerContainer: {
        borderWidth: 2,
        borderColor: '#d1d5db',
        borderRadius: 12,
        backgroundColor: '#fff',
    },
    button: {
        backgroundColor: '#16a34a',
        borderRadius: 12,
        padding: 18,
        alignItems: 'center',
        marginTop: 12,
        marginBottom: 16,
    },
    buttonDisabled: {
        backgroundColor: '#9ca3af',
    },
    buttonText: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold',
    },
    linkText: {
        color: '#16a34a',
        textAlign: 'center',
        fontSize: 14,
        fontWeight: '600',
    },
});

export default RegisterScreen;
