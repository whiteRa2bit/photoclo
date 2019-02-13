<template>
    <div>
        <div style="height:80vh; text-align: center">
            <gallery v-bind:images="images" v-bind:imagesBig="imagesBig" v-bind:avatars="avatars" />
        </div>
    </div>

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
                imagesBig: [],
                avatars: [],
                index: null
            }
        },
        mounted() {
            var this_ = this;
            axios.get('http://photoclo.ru:8000/api/photos/', { headers: {Authorization: "Token " + localStorage.token}, params: {offset: 0, limit: 2000, size: "m"}}).then(function (response) {
                for (var i = 0; i < response.data.photos.length; ++i) {
                    this_.images.push(response.data.photos[i]);
                }
                console.log(response);
            }).catch(function (error) {
                console.log(error);
            });
            axios.get('http://photoclo.ru:8000/api/photos/', { headers: {Authorization: "Token " + localStorage.token}, params: {offset: 0, limit: 2000, size: "o"}}).then(function (response) {
                for (var i = 0; i < response.data.photos.length; ++i) {
                    this_.imagesBig.push(response.data.photos[i]);
                }
                console.log(response);
            }).catch(function (error) {
                console.log(error);
            });
            axios.get('http://photoclo.ru:8000/api/avatars/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
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
                axios.get('http://photoclo.ru:8000/api/photos/', { headers: {Authorization: "Token " + localStorage.token}, params: {offset: 0, limit: 2000, size: "m"}}).then(function (response) {
                    this_.images = [];
                    for (var i = 0; i < response.data.photos.length; ++i) {
                        this_.images.push(response.data.photos[i]);
                    }
                }).catch(function (error) {
                    console.log(error);
                });
                axios.get('http://photoclo.ru:8000/api/photos/', { headers: {Authorization: "Token " + localStorage.token}, params: {offset: 0, limit: 2000, size: "o"}}).then(function (response) {
                    this_.imagesBig = [];
                    for (var i = 0; i < response.data.photos.length; ++i) {
                        this_.imagesBig.push(response.data.photos[i]);
                    }
                }).catch(function (error) {
                    console.log(error);
                });
                axios.get('http://photoclo.ru:8000/api/avatars/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
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
    .mySpan {
        top: 50% !important;
    }
</style>
