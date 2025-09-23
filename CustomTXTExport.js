tiled.registerMapFormat("CustomTXT", {
    name: "Custom TXT Export",
    extension: "txt",

    write: function(map, fileName) {
		const tileset = map.tilesets[0];
        let output = "";

        for (let i = 0; i < map.layerCount; ++i) {
			const layer = map.layerAt(i);
			
            if (!layer.isTileLayer) {
				continue;
			}

            for (let y = 0; y < layer.height; ++y) {
                for (let x = 0; x < layer.width; ++x) {
					const cell = layer.cellAt(x, y);
					const masterTile = tileset.tile(cell.tileId);
					output += masterTile.property("Symbol");
                }
				
                output += "\n";
            }
        }

        const file = new TextFile(fileName, TextFile.WriteOnly);
        file.write(output);
        file.commit();
    }
});
