import axios from 'axios'

const AXIOS = axios.create({
    baseURL: '/api/subscription'
});

export default {
    subscribeKeyword(keyword) {
        return AXIOS.post(`${keyword}`);
    }
}


