#!/bin/bash

if [ "$REQUEST_METHOD" = "POST" ] ; then
  if [ "$CONTENT_LENGTH" -gt 0 ] ; then
      read -n $CONTENT_LENGTH POST_BODY <&0
  fi
fi

ACTION_TYPE=$(echo $POST_BODY | awk -F "request=" '{print $2}')

if [ "$ACTION_TYPE" = "LOGIN" ] ; then 
  USER_ID=$(echo $POST_BODY | awk -F'[=&]' {'print $2'})
  PASSWORD=$(echo $POST_BODY | awk -F'[=&]' {'print $4'})
  
  XML_CONTENT="<logininfo><userid>$USER_ID</userid><passwordhash>$PASSWORD</passwordhash></logininfo>"
  RESPONSE=$(curl -i --request POST --cookie "$HTTP_COOKIE" --url "http://172.17.0.2:3000/login" --header 'content-type: text/xml' --data "$XML_CONTENT" | grep Cookie)
  
  COOKIE=$(echo "$RESPONSE" | awk -F'[:;]' {'print $2'})
        
# echo "Set-cookie:$COOKIE"        
  echo "Content-type:text/html;charset=utf-8"
  echo
else
  echo "Content-type:text/html;charset=utf-8"
  echo  
fi


cat << EOF
<!doctype html>
<html>
<head>
<title>CGI</title>
<style>
	form {
  			border: 3px solid #f1f1f1;
		}
		h1{
  			color: #4f92ff;
		}
    h4{
  			color: #4f92ff;
		}
		button {
			background-color: #4f92ff;
			color: white;
			padding: 15px 32px;
			text-align: center;
			display: inline-block;
			font-size: 16px;
			margin: 8px 0;
			cursor: pointer;
		}
		input{
			background-color: #e8f0ff;
		}
	</style>
</head>
<body>
	<h1>Biblioteket</h1>
  <h4>abaklien, vknudsen, llundberg og vsteinsto</h4>
 <form method=POST>
  <div class="container">
    <input type="text" placeholder="Username" name="uname" required>
    <input type="password" placeholder="Password" name="psw" required>
    <button type="submit" name="request" value="LOGIN">Login</button>
  </div>
</form> 
<form method=POST>
  	<select name=table>
  		<option value="authors">Authors</option>
  		<option value="books">Books</option>
  	</select><br><br>
  <input type="text" placeholder="ID" name="id"><br>
  <input type="text" placeholder="Parameter 1" name="param1"><br>
  <input type="text" placeholder="Parameter 2" name="param2"><br>
  <input type="text" placeholder="Parameter 3" name="param3"><br>
  <input type="radio" name="action" value="GET" checked> Search<br>
  <input type="radio" name="action" value="PUT"> Edit<br>
  <input type="radio" name="action" value="POST"> Add<br>
  <input type="radio" name="action" value="DELETE"> Delete<br>
  <button type="submit">Submit</button>
</form>
</body>
</html>
EOF

/usr/bin/env | grep $REQUEST_METHOD

  TABLE=`echo "$QUERY_STRING" | sed -n 's/^.*table=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
  ID=`echo "$QUERY_STRING" | sed -n 's/^.*id=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
  REQ=`echo "$QUERY_STRING" | sed -n 's/^.*action=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
  PARAM1=`echo "$QUERY_STRING" | sed -n 's/^.*param1=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
  PARAM2=`echo "$QUERY_STRING" | sed -n 's/^.*param2=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
  PARAM3=`echo "$QUERY_STRING" | sed -n 's/^.*param3=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

  if [[ "$REQ" == *"GET"* ]] ; then
    resp=$(curl --request $REQ "http://172.17.0.2:3000/$TABLE/$ID")
    echo '<br>'
  fi
  if [[ "$REQ" == *"POST"* ]] ; then
    if [[ "$TABLE" == *"authors"* ]] ; then
      resp=$(curl --data "authorID=$ID&firstname=$PARAM1&lastname=$PARAM2&nationality=$PARAM3" -X $REQ "http://172.17.0.2:3000/authors")
    elif [[ "$TABLE" == *"books"* ]] ; then
      resp=$(curl --data "bookID=$ID&booktitle=$PARAM1&authorID=$PARAM2" -X $REQ "http://172.17.0.2:3000/books")
    fi
    echo '<br>'
  fi
  if [[ "$REQ" == *"PUT"* ]] ; then
    if [[ "$TABLE" == *"authors"* ]] ; then
      resp=$(curl --data "authorID=$ID&firstname=$PARAM1&lastname=$PARAM2&nationality=$PARAM3" -X $REQ "http://172.17.0.2:3000/authors")
    elif [[ "$TABLE" == *"books"* ]] ; then
      resp=$(curl --data "bookID=$ID&booktitle=$PARAM1&authorID=$PARAM2" -X $REQ "http://172.17.0.2:3000/books")
    else
      echo "Table name incorrect!"
    fi
    echo '<br>'
  fi
  if [[ "$REQ" == *"DELETE"* ]] ; then
    if [[ "$TABLE" == *"authors"* ]] ; then
      resp=$(curl --data "authorID=$ID" -X $REQ "http://172.17.0.2:3000/authors")
    elif [[ "$TABLE" == *"books"* ]] ; then
      resp=$(curl --data "bookID=$ID" -X $REQ "http://172.17.0.2:3000/books")
    else
      echo "WRONG!"
    fi
    echo '<br>'
  fi
  echo '<br>'
  echo $resp
  echo '<br>'
fi
