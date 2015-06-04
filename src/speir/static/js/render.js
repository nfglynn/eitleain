var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75,
					 window.innerWidth / window.innerHeight,
					 0.1,
					 1000);

var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

var geometry = new THREE.BoxGeometry(0.1, 0.1, 0.1);
var material = new THREE.MeshBasicMaterial({color: 0x00ff00});

var cube = new THREE.Mesh(geometry, material);

scene.add(cube);

camera.position.z = 5;

aircraft = 
function receive(data) {
    console.log(data);
}

function render() {
    $.ajax({
	url: "/speir/all",
	success: receive,
    });
    camera.rotation.z += 0.05
    cube.rotation.x += 0.1;
    cube.rotation.y += 0.1;
    requestAnimationFrame( render );
    renderer.render( scene, camera );
}

render();
