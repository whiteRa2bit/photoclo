<template>
    <img id="imageItem" v-bind:src="imageURL" alt=""/>
</template>

<script>
    
	export default {
		name: 'imageItem',
		props: ['imageURL'],
		methods: {}
	}
</script>

<style scoped>
    #imageItem {
    	border: 0px black;
        margin: 5px;
    }

    #imageItem:hover {
    	opacity: 0.8;
    	cursor: pointer;
    }
</style>