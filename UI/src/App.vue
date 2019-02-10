<template>

    <div id="app">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

        <b-navbar v-if="authenticated" toggleable="md" type="dark" variant="info">

            <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

            <b-navbar-brand href="photoclo.ru:8000">PHOTOCLO</b-navbar-brand>

            <b-collapse is-nav id="nav_collapse">



                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">

                    <!--     Search     -->
                    <!--<form class="form-inline md-form form-sm mt-0">-->
                        <!--<i class="fas fa-search" aria-hidden="true"></i>-->
                        <!--<input class="form-control form-control ml-3 w-75" type="text" placeholder="Поиск" aria-label="Search">-->
                    <!--</form>-->

                    <div id="uploadIcon" v-on:click="startUpload">
                        <div id="uploadImg" v-on:click="updateToken()" slot="button-content"><img src="https://i.ibb.co/KxpYbZc/Webp-net-resizeimage-5.png" /></div>
                        <b-button id="uploadButton" ref="uploadButton" v-b-modal.uploadModal class="mr-sm-2" v-on:click="updateToken(); isModalShown = true; resetUploader()" right>Загрузить</b-button>
                    </div>
                    <!--<span> myUploader.data().toClose </span>-->
                    <b-modal id="uploadModal" ref="uploadModal" hide-footer=true title="Загрузка фотографий">
                        <myUploader ref="myUploader" v-on:closeModal="isModalShown = false;" url="http://photoclo.ru:8000/api/photos/" @upload-image-success='updateImages();' @upload-image-failure='updateImages();'> </myUploader>
                    </b-modal>

                    <div id="yandexDiskIcon">
                        <div id="yandexDiskImg"><img src="https://i.ibb.co/QbRbLYx/rsz-yandex-icon.png" class="d-inline-block align-top"></div>
                        <span> Яндекс.Диск </span>
                    </div>

                    <div id="userIcon">
                        <b-dropdown id="userButton" right text="Пользователь"  class="mr-sm-2" no-caret variant="link">
                            <div id="userImg" slot="button-content"><img src="https://i.ibb.co/rHPWQ14/Webp-net-resizeimage-4.png" /></div>
                            <b-dropdown-item href="#">Профиль</b-dropdown-item>
                            <b-dropdown-item v-on:click="logout()">Выйти</b-dropdown-item>
                        </b-dropdown>
                    </div>
                </b-navbar-nav>

            </b-collapse>
        </b-navbar>
        <router-view @authenticated="setAuthenticated" ref="child" />
    </div>
</template>

<script>
    import axios from 'axios';
    import MultipleFileUploader from './components/MultipleFileUploader.vue';
    import myUploader from './components/myUploader.vue'
    var modal = document.getElementById('id01');

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    window.onload = function() {
        var this_ = this;
        document.getElementsByClassName('myUploader')[0].__vue__.$props.my_header = {Authorization: "Token " + localStorage.token};
    }

    export default {
        name: 'App',
        data() {
            return {
                authenticated: false,
                token: undefined,
                isModalShown: false,
            }
        },
        components: {
            MultipleFileUploader,
            myUploader
        },
        watch: {
            isModalShown(value) {
                if (value) {
                    this.$refs.uploadModal.show();
                }
                else {
                    this.$refs.uploadModal.hide();
                }
            }
        },
        mounted() {

            if (localStorage.hasOwnProperty('token')) {
                this.token = localStorage.token;
                this.authenticated = true;
            }
            if(!this.authenticated) {
                this.$router.replace({ name: "login" });
            }
            else {
                var this_ = this;
                this.$router.replace({name: "secure"});
            }
        },

        methods: {
            updateToken () {
                document.getElementsByClassName('myUploadBox')[0].__vue__.$props.my_header = {Authorization: "Token " + localStorage.token};
            },
            setAuthenticated(status) {
                this.authenticated = status;
            },
            logout() {
                var this_ = this;
                axios.post('http://photoclo.ru:8000/api/sign_out/', {Authorization: "Token " + String(this.token)}).then(function () {
                    this_.authenticated = false;
                    this_.$router.replace({ name: "login" });
                    delete localStorage.token;
                });
            },
            updateImages() {
                this.$refs.child.updateImages();
            },
            resetUploader() {
                this.$refs.myUploader.resetUploader();
            },
            startUpload() {
                this.$refs.uploadButton.click();
            }
        },
    }
</script>

<style>
    body {
        background-color: #E0E0E0;
        background-image: url("background.jpg");
    }
    h1 {
        padding: 0;
        margin-top: 0;
    }
    #app {
    }

    .active {
        background-color: #4CAF50;
        color: white;
    }

    button:hover {
        opacity: 0.8;
    }

    .dropAreaDragging{
        background-color: #ccc;
    }

    .searchbar{
        margin: auto;
        height: 60px;
        background-color: #353b48;
        border-radius: 30px;
        padding: 10px;
    }

    .search_input{
        color: white;
        border: 0;
        outline: 0;
        background: none;
        width: 0;
        line-height: 40px;
        transition: width 0.4s linear;
    }

    .searchbar:hover > .search_input{
        padding: 0 10px;
        width: 200px;
        transition: width 0.4s linear;
    }

    .searchbar:hover > .search_icon{
        background: white;
        color: #e74c3c;
    }

    .search_icon{
        height: 40px;
        width: 40px;
        float: right;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 50%;
        color:white;
    }
    #userButton {

    }
    #yandexDiskIcon {
        display: flex;
        flex-direction: column;
        text-align: center;
        margin-right: 20px;
        margin-left: 20px;
    }
    #yandexDiskImg {

    }
    #uploadIcon {
        display: flex;
        flex-direction: column;
        text-align: center;
        cursor: pointer;
    }
    #userImg {
        height: auto;
        width: auto;
    }
    #uploadButton {
        height: auto;
        font-size: 12px;
        color: black;
        background-color: white;
        text-align: center;
    }
</style>

