<template>
    <div id="app">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div v-if="authenticated" class="topnav" id="myTopnav">
            <a href="photoclo.ru:8000">PHOTOCLO</a>
            <div class="searchField">
                <br>
                <input type="text" class="input" id="searchField" name="search" v.model="input.search" v-on:change="updateSearch" required tabindex="1" />
                <span class="floating-label">Поиск</span>
            </div>
            <div class="leftButtons">
                <button id="uploadButton" onclick="document.getElementById('id01').style.display='block'" style="width:auto;">upload</button>

                <div id="id01" class="modal">
                    <div class="modal-content">
                        <div class="container">
                            <multiple-file-uploader id="fileUploader" postURL="/api/photos/" successMessagePath="" errorMessagePath=""></multiple-file-uploader>
                        </div>

                        <div class="container" style="background-color:#f1f1f1">
                          <button type="button" onclick="document.getElementById('id01').style.display='none'" class="cancelButton">Close</button>
                        </div>
                    </div>
                </div>

                <button id="logoutButton" type="button" v-on:click="logout()">logout</button>
                <a href="javascript:void(0);" class="icon" v-on:click="myFunction()">
                    <i class="fa fa-bars"></i>
                </a>
            </div>
        </div>
        <router-view @authenticated="setAuthenticated" />
    </div>
</template>

<script>
    import axios from 'axios';
    import MultipleFileUploader from '@updivision/vue2-multi-uploader';

    var modal = document.getElementById('id01');

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    window.onload = function() {
        var this_ = this;
        var element = document.getElementsByClassName('uploadBox')[0];
        element.__vue__.$props.postHeader = {Authorization: "Token " + localStorage.token};
    }

    export default {
        name: 'App',
        data() {
            return {
                authenticated: false,
                token: undefined,
            }
        },
        components: {
            MultipleFileUploader
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
            setAuthenticated(status) {
                this.authenticated = status;
            },
            logout() {
                var this_ = this;
                axios.post('/api/sign_out/', {Authorization: "Token " + String(this.token)}).then(function () {
                    this_.authenticated = false;
                    this_.$router.replace({ name: "login" });
                    delete localStorage.token;
                });
                /*this_.authenticated = false;  
                delete localStorage.token;*/
            },
            myFunction() {
                var x = document.getElementById("myTopnav");
                if (x.className === "topnav") {
                    x.className += " responsive";
                } else {
                    x.className = "topnav";
                }
            },
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

    .topnav {
        width: 100%;
        background-color: #FFF;
        overflow: hidden;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-content: center;
    }

    .topnav a {
        float: left;
        display: block;
        color: #3A78DE;
        text-align: center;
        padding: 20px 16px;
        text-decoration: none;
        font-size: 20px;
    }

    .topnav a:hover {
        background-color: #ddd;
        color: black;
    }

    .active {
        background-color: #4CAF50;
        color: white;
    }

    .topnav .icon {
        display: none;
    }

    @media screen and (max-width: 600px) {
        .topnav a:not(:first-child) {display: none;}
        .topnav a.icon {
            float: right;
            display: block;
        }
    }

    @media screen and (max-width: 600px) {
        .topnav.responsive {position: relative;}
        .topnav.responsive a.icon {
            position: absolute;
            right: 0;
            top: 0;
        }
        .topnav.responsive a {
            float: none;
            display: block;
            text-align: left;
        }
    }

    .searchField {
        align-self: center;
    }

    #logoutButton,
    .cancelButton,
    #uploadButton {
        background-color: #4CAF50;
        color: white;
        padding: 14px 20px;
        margin: 8px 0;
        border: none;
        cursor: pointer;
    }

    .cancelButton,
    #uploadButton {
        width: 100%;
    }

    button:hover {
      opacity: 0.8;
    }

    .cancelButton {
      width: auto;
      padding: 10px 18px;
      background-color: #f44336;
    }

    .container {
      padding: 16px;
    }

    .modal {
        display: none;
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgb(0,0,0);
        background-color: rgba(0,0,0,0.4);
        padding-top: 60px;
    }

    .modal-content {
        background-color: #fefefe;
        margin: 5% auto 15% auto;
        border: 1px solid #888;
        width: 80%;
    }

    .animate {
        -webkit-animation: animatezoom 0.6s;
        animation: animatezoom 0.6s
    }

    @-webkit-keyframes animatezoom {
        from {-webkit-transform: scale(0)} 
        to {-webkit-transform: scale(1)}
    }
      
    @keyframes animatezoom {
        from {transform: scale(0)} 
        to {transform: scale(1)}
    }

    @media screen and (max-width: 300px) {
        span.psw {
            display: block;
            float: none;
        }
        .cancelbtn {
            width: 100%;
        }
    }

    .dropAreaDragging{
        background-color: #ccc;
    }

    .input {
        font: 20px Calibri;
        border-left: 0px;
        border-right: 0px;
        border-top: 0px;
        border-bottom: 1px solid #3A78DE;
    }

    input:focus {
        outline: none !important;
    }

    .searchField {
        position: relative;
        width: 50%;
    }
    .searchField .input{
        width: 100%;
        outline: none;
        border:none;
        border-bottom: 1px solid #3A78DE;
    }
    .searchField .input:invalid {
        box-shadow: none !important;
        border-bottom: 1px solid red;
    }
    .searchField .input:focus{
        border-width: medium medium 2px;
    }
    .searchField .floating-label {
        position: absolute;
        pointer-events: none;
        top: 20px;
        left: 5px;
        transition: 0.15s ease all;
        color: #777;
    }
    .searchField input:focus ~ .floating-label,
    .searchField input:not(:focus):valid ~ .floating-label{
        top: 5px;
        left: 2px;
        font-size: 13px;
        opacity: 1;
        color: #000;
    }

    .leftButtons {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
</style>