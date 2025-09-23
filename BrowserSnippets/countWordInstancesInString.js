const countWordInstancesInString = (rawString) =>
	rawString
		.split('\n')
		.reduce((p, c) => [...p, ...c.split(",")], [])
		.map(s => s.trim())
		.reduce((p, c, i, a) => p.set(c, a.filter(s => s === c).length), new Map([]))
		.entries()
		.toArray();
		