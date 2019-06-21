import axios from 'axios'

const AXIOS = axios.create({
    baseURL: '/api/subscription'
});

export default {
    subscribeKeyword(keyword, username) {
        return AXIOS.post(`${keyword}`, null, {
            params: {
                username: username
            }
        });
    }
}


