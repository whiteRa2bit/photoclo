<template>
    <gallery v-bind:images="images" v-bind:avatars="avatars" />
</template>

<script>

    import gallery from './gallery.vue';
    import uploader from 'vue-simple-uploader';
    import axios from 'axios';
    
    import imageItem from './imageItem.vue'; 

    export default {
        components: {
            gallery,
            imageItem
        },
        name: 'Secure',
        data() {
            return {
                images: [],
                avatars: [],
                index: null
            }
        },
        mounted() {
            var this_ = this;
            axios.get('/api/photos/', { headers: {Authorization: "Token " + localStorage.token}, params: {offset: 0, limit: 2000, size: "z"}}).then(function (response) {
                for (var i = 0; i < response.data.photos.length; ++i) {
                    this_.images.push(response.data.photos[i]);
                }
            }).catch(function (error) {
                console.log(error);
            });
            axios.get('/api/avatars/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
                for (var i = 0; i < response.data.avatars.length; ++i) {
                    this_.avatars.push(response.data.avatars[i]);
                }
            }).catch(function (error) {
                console.log(error);
            });
        },
        methods: {
            updateImages() {
                var this_ = this;
                axios.get('/api/photos/', { headers: {Authorization: "Token " + localStorage.token}, params: {offset: 0, limit: 2000, size: "z"}}).then(function (response) {
                    this_.images = [];
                    for (var i = 0; i < response.data.photos.length; ++i) {
                        this_.images.push(response.data.photos[i]);
                    }
                }).catch(function (error) {
                    console.log(error);
                });
                axios.get('/api/avatars/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
                    this_.avatars = [];
                    for (var i = 0; i < response.data.avatars.length; ++i) {
                        this_.avatars.push(response.data.avatars[i]);
                    }
                }).catch(function (error) {
                    console.log(error);
                });
            }
        }
    }
</script>

<style scoped>
</style>
