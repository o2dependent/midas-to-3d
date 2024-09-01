<script lang="ts">
	import {
		Engine,
		Color3,
		Scene,
		Vector3,
		HemisphericLight,
		Mesh,
		ArcRotateCamera,
		PointLight,
		Color4,
		VideoRecorder,
		MeshBuilder,
		StandardMaterial,
	} from "@babylonjs/core";
	import { onMount } from "svelte";
	onMount(async () => {
		const res = await fetch("/midas_data.json");
		const json = await res.json();
		const width = json.width as number;
		const height = json.height as number;
		const data = json.data as number[][];

		const canvas = document.querySelector(
			"#babylon-canvas",
		) as HTMLCanvasElement;
		const engine = new Engine(canvas);

		// Creates a basic Babylon Scene object
		const scene = new Scene(engine);
		// Creates and positions a free camera
		const camera = new ArcRotateCamera(
			"Camera",
			0,
			Math.PI / 2,
			20,
			Vector3.Zero(),
			scene,
		);
		// Targets the camera to scene origin
		camera.setTarget(Vector3.Zero());
		// Attaches the camera to the canvas
		camera.attachControl(canvas, true);
		// Creates a light, aiming 0,1,0
		const light = new HemisphericLight("light", new Vector3(1, 0, 0), scene);
		// Dim the light a small amount 0 - 1
		light.intensity = 0.7;

		const initPaths = [];
		const paths = [];
		const colors: Color4[] = [];
		for (let j = 0; j < data[0].length; j += 1) {
			const path: Vector3[] = [];
			const initPath: Vector3[] = [];

			for (let i = 0; i < data.length; i += 1) {
				let x = (j / data.length) * -10;
				let y = (i / data[0].length) * -10;
				let z = data[i][j] / 100;
				if (i === 0 || i === data.length - 1) z = 0;
				path.push(new Vector3(x, y, z));
				initPath.push(new Vector3(x, y, 0));
			}

			paths.push(path);
			initPaths.push(initPath);
			var r = 0.5 + Math.random() * 0.2;
			var g = 0.5 + Math.random() * 0.4;
			var b = 0.5;
			colors.push(new Color4(r, g, b, 1));
		}

		const ribbon = MeshBuilder.CreateRibbon("ribbon", {
			pathArray: paths,
			closePath: true,
			// sideOrientation: Mesh.DOUBLESIDE,
			sideOrientation: Mesh.FLIP_TILE,
			updatable: true,
		});
		ribbon.rotate(new Vector3(0, 1, 0), Math.PI / 2);
		const neonMaterial = new StandardMaterial("neonMaterial", scene);
		// neonMaterial.emissiveColor = Color3.Teal();
		ribbon.material = neonMaterial;
		// ribbon.material.wireframe = true;

		let elapsedTime = 0;

		window.addEventListener("resize", () => {
			engine.resize();
		});

		engine.runRenderLoop(() => {
			const engine = scene.getEngine();
			elapsedTime += engine.getDeltaTime();
			// this.nodes.forEach((node) => node?.update?.(elapsedTime));

			// if (this.cameraLight && this.flashLight && scene?.activeCamera) {
			// 	this.flashLight.position = scene?.activeCamera?.position;
			// }

			scene.render();
		});
	});
</script>

<canvas
	style="width: 100%; height: 100vh;"
	id="babylon-canvas"
	width="100%"
	height="100vh"
></canvas>
