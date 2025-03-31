import axios from 'axios';
import { toast } from 'vue3-toastify';

export async function login(email, password, usertype) {

    return await axios.post('http://127.0.0.1:5000/api/v2/login', {
        email,
        password,
        usertype
    })
    .then(response => {
        localStorage.setItem('token', response.data.token || "");
        return response.data;
    })
    .catch(error => {
        
        toast('An error occurred during login.', { type: 'error' });
        console.error('Login failed:', error);
        throw error;
    });
}


export async function customerRegister(email, password,full_name, phone, address,pin_code) {
    console.log('Registering with Email:', email,password,full_name, phone, address,pin_code);
    return await axios.post('http://127.0.0.1:5000/api/v2/signup/customer', {
        email,
        password,
        full_name,
        phone,
        address,
        pin_code
    })
    .then(response => {
        
        return response.data;
    })
    .catch(error => {
        console.log(error)
        
        toast(error.response.data.message, { type: 'error' });
        console.error('Registration failed:', error);
        throw error;
    });
}

export async function professionalRegister(email, password,full_name, phone, address,pin_code,service_name,experience) {
    console.log('Registering with Email:', email,password,full_name, phone, address,pin_code,service_name,experience);
    return await axios.post('http://127.0.0.1:5000/api/v2/signup/professional', {
        email,
        password,
        full_name,
        phone,
        address,
        pin_code,
        service_name,
        experience
    })
    .then(response => {
        
        toast('Registration successful!', { type: 'success' });
        return response.data;
    })
    .catch(error => {
        
        toast('An error occurred during registration.', { type: 'error' });
        console.error('Registration failed:', error);
        throw error;
    });

}

// Add logout function
export function logout() {
    localStorage.removeItem('token'); // Remove token from localStorage
    toast('Logged out successfully', { type: 'success' }); // Show success message
}
