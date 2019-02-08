<template>
	<div class="myContainer">
    	<img id="image-WBB-Item" v-bind:src="image.url" alt="" />
        <bbButton class="btn" v-for="(face, index) in faces" v-bind:srcWidth="image.width" v-bind:srcHeight="image.height" v-bind:face="face" v-bind:ids="index" />
    </div>
</template>

<script>
    import bbButton from './bbButton.vue';

	export default {
		name: 'imageWBBItem',
        components: {
            bbButton
        },
		props: {
            image: {
                type: Object,
                default () {
                    return {};
                }
            },
            faces: {
                type: Object,
                default() {
                    return {};
                }
            }
        },
        methods: {}
	}
</script>

<style scoped>
    #image-WBB-Item {
        margin: auto;
        overflow: auto;
        display: block;
    }

    .myContainer {
    }

    /* Make the image responsive */
    .myContainer img {
        width: 100%;
        height: auto;
    }

    /* Style the button and place it in the middle of the container/image */
    .myContainer .btn {
        position: absolute;
        transform: translate(-50%, -50%);
        -ms-transform: translate(-50%, -50%);
        border: none;
        cursor: pointer;    
    }

    .myContainer .btn:hover {
        background-color: black;
    }
</style>