<template>
    <div class='flex-container-button'>
        <button class='point-button' @click="sendCommand('point A')">Point A</button>
        <button class='point-button' @click="sendCommand('point B')">Point B</button>
        <button class='point-button' @click="sendCommand('point C')">Point C</button>
    </div>
</template>

<style>
    .flex-container-button {
        display: flexbox;
        justify-content: center;
        place-items: center;
        flex-direction: column;
        padding-top:20px;
    }
    .point-button {
        margin: 10px;
        padding: 10px;
        border-radius: 4px;
        border: 1px solid #ddd;
        background-color: #fff;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    
    }
</style>
<script>
// import axios from 'axios';

export default {
    name: 'AutomaticControl',
    props: {
        msg: String,
        ws: {
            type: Object,
            required: true
        }
    },
    methods: {
        sendCommand(point) {
            console.log(process.env.VUE_APP_WS_URL, point);
            // axios.post(`${process.env.VUE_APP_API_URL}/point`, {
            //     point: point
            // }).then(response => {
            //     console.log(response.data)
            // }).catch(error => {
            //     console.log(error)
            // })
        }
    }
}
</script>