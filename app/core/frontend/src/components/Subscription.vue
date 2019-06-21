<template>
    <div>
        <form @submit.prevent="subscribeKeyword()">
            <input type="text" placeholder="keyword" v-model="keyword">
            <b-btn class="ml-1" variant="success" type="submit">Subscribe</b-btn>
            <p v-if="success" class="alert-success">Successful subscribed <span style="font-weight: bold;">{{ keyword }}</span></p>
            <p v-if="error" class="error">Problem with server</p>
        </form>

    </div>
</template>

<script>
    import subscriptionApi from "./subscription-api";
    import store from '../store'

    export default {
        name: "Subscription",
        data () {
            return {
                success: false,
                error: false,
                keyword: ''
            }
        },
        methods: {
            subscribeKeyword() {
                subscriptionApi.subscribeKeyword(this.keyword, store.getters.username).then(response => {
                    this.error = false;
                    this.success = response.data;
                    console.log('success');
                }).catch(error => {
                    this.error = true;
                });
            }
        }
    }
</script>

<style scoped>

</style>