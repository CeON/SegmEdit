<html>
<head>
	<title>Summary</title>
	<style>
table {
	empty-cells: show;
}
.status-error {
	background: #f66;
}
.status-complete {
	background: #6f6;
}
.status-unlocked {
	background: #ccc;
}
.status-locked {
	background: #99f;
}
	</style>
</head>
<body>
	<h1>Summary</h1>
	
	<dl>
		<dt>Unlocked</dt>
		<dd>{{unlocked}}</dd>
		<dt>Locked</dt>
		<dd>{{locked}}</dd>
		<dt>Complete</dt>
		<dd>{{complete}}</dd>
		<dt>Error</dt>
		<dd>{{error}}</dd>
	</dl>
	
	<table border="1">
		<tr>
			<th>ISSN</th>
			<th>Title</th>
			<th>Status</th>
			<th>Last user</th>
			<th>Comment</th>
		</tr>
%for document in documents:
		<tr>
			<td>{{document.id}}</td>
			<td>{{document.text}}</td>
			<td class="status-{{document.status}}">{{document.status}}</td>
			<td>{{document.username or ''}}</td>
			<td>{{document.comment}}</td>
		</tr>
%end
	</table>
</body>	
</html>