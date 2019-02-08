<template>
    <form id="login" align="center">
        <h1>Вход</h1>
        <div class="inputFields">
            <span class="error" v-if="empty">*Все поля должны быть заполнены.</span>
            <span class="error" v-if="incorrect">*Логин или пароль введены не верно.</span>
            <div class="user-input-wrp">
                <br/>
                <input
                        type="text"
                        class="input"
                        id="loginField"
                        name="username"
                        ref="username"
                        v.model="input.username"
                        v-on:keyup.enter="login"
                        v-on:change="updateUsername">
                <span class="floating-label">Логин</span>
            </div>
            <div class="user-input-wrp">
                <br/>
                <input
                        type="password"
                        class="input"
                        id="passwordField"
                        name="password"
                        ref="password"
                        v.model="input.password"
                        v-on:keyup.enter="login"
                        v-on:change="updatePassword"
                        required tabindex="2" />
                <span class="floating-label">Пароль</span>
            </div>
            <button class="button" id="loginButton" form="login" type="button" v-on:keyup.enter="login" v-on:click="login()" tabindex="3"><span>Вход</span></button>
        </div>
        <button class="button" id="registerButton" form="login" type="button" v-on:click="toRegisterPage()" tabindex="4">Еще нет аккаунта? Зарегистрируйтесь!</button>
    </form>
</template>

<script>
    import axios from 'axios';
    export default {
        name: 'Login',
        data() {
            return {
                empty: true,
                incorrect: false,
                info: "",
                input: {
                    username: null,
                    password: null
                }
            }
        },
        methods: {
            login() {
                if (!(this.input.username && this.input.password)) {
                    if (!this.input.username) {
                        this.$refs.username.focus()
                    } else {
                        this.$refs.password.focus()
                    }
                } else {
                    var this_ = this;
                    axios.post('/api/sign_in/', {username: this.input.username,
                        password: this.input.password})
                        .then(function (response) {
                            localStorage.token = response.data.token;
                            this_.$emit("authenticated", true);
                            this_.$router.replace({ name: "secure" });
                        }).catch(function (error) {
                        console.log(error);
                        this_.incorrect = true;
                    });

                }
            },
            toRegisterPage() {
                this.$router.replace({ name: "register" });
            },
            updateUsername(event) {
                this.input.username = event.target.value;
                this.incorrect = false;
                if (this.input.username == "" || this.input.password == "") {
                    this.empty = true;
                }
                else {
                    this.empty = false;
                }
            },
            updatePassword(event) {
                this.input.password = event.target.value;
                this.incorrect = false;
                if (this.input.username == "" || this.input.password == "") {
                    this.empty = true;
                }
                else {
                    this.empty = false;
                }
            }
        }
    }
</script>

<style scoped>
    #login {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        width: 30%;
        min-width: 300px;
        border: 1px solid #CCCCCC;
        background-color: #FFFFFF;
        margin: auto;
        margin-top: 5vh;
        height: 80vh;
        min-height: 350px;
        padding: 20px;
        font: 20px Calibri;
    }

    .input {
        font: 20px Calibri;
        border-left: 0px;
        border-right: 0px;
        border-top: 0px;
        border-bottom: 1px solid #3A78DE;
    }

    .button {
        width: 75%;
        font: 20px Calibri;
        color: #FFFFFF;
        border-radius: 2px;
        padding: 4px;
        border: 0px;
        margin: 10px;
        cursor: pointer;
        outline: none !important;
        background-color: #FFF;
    }

    button:hover {
        opacity: 0.8;
    }

    button:focus {
        outline: none !important
    }

    #loginButton {
        background-color: #3A78DE;
        color: white;
        box-shadow: 0.1em 0.1em 5px rgba(122,122,122,0.5);
        transition: all 0.5s;
        cursor: pointer;
    }
    #loginButton span {
        cursor: pointer;
        display: inline-block;
        position: relative;
        transition: 0.5s;
    }

    #loginButton span:after {
        content: '\00bb';
        position: absolute;
        opacity: 0;
        top: 0;
        right: -20px;
        transition: 0.5s;
    }

    #loginButton:focus span,
    #loginButton:hover span {
        padding-right: 25px;
    }

    #loginButton:focus span:after,
    #loginButton:hover span:after {
        opacity: 1;
        right: 0;
    }

    #registerButton{
        text-align: left;
        font-size: 15px;
        color: #3A78DE;
    }

    input:focus {
        outline: none !important;
    }
    .inputFields {
        width: 100%;
        display: flex;
        align-items: center;
        flex-direction: column;
    }
    .user-input-wrp {
        position: relative;
        width: 75%;
    }
    .user-input-wrp .input{
        width: 100%;
        outline: none;
        border:none;
        border-bottom: 1px solid #3A78DE;
    }
    .user-input-wrp .input:invalid {
        box-shadow: none !important;
        border-bottom: 1px solid red;
    }
    .user-input-wrp .input:focus{
        border-width: medium medium 2px;
    }
    .user-input-wrp .floating-label {
        position: absolute;
        pointer-events: none;
        top: 18px;
        left: 5px;
        transition: 0.15s ease all;
        color: #777;
    }
    .user-input-wrp input:focus ~ .floating-label,
    .user-input-wrp input:not(:focus):valid ~ .floating-label{
        top: 5px;
        left: 0px;
        font-size: 13px;
        opacity: 1;
        color: #000;
    }
    .error {
        font: 13px Colibri;
        width: 75%;
        color: red;
        text-align: left;
    }
</style>