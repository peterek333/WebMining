import axios from 'axios'

const AXIOS = axios.create({
    baseURL: '/api/notification'
});

export default {
    getNotifications(username) {
        return AXIOS.get(`${username}`);
    },
    popNotifications(username) {
        return AXIOS.get(`/pop/${username}`);
    }
}


