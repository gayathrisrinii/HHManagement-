import axios from 'axios';
import { toast } from 'vue3-toastify';

export async function addServices(service_name, description,category,base_price) {

    console.log('Logging in with Email:', service_name);

    return await axios.post('http://127.0.0.1:5000/api/v2/admin/services', {
        service_name, description,category,base_price
    })
    .then(response => {
        
        toast('Service created successfully!', { type: 'success' });
        return response.data;
    })
    .catch(error => {
        
        toast('An error occurred during creating service.', { type: 'error' });
        console.error('Login failed:', error);
        throw error;
    });
}
