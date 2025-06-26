
// App.jsx - Mock React frontend (with issues)
import React, { useState, useEffect } from 'react';

function App() {
  const [feedback, setFeedback] = useState([]);
  const [rating, setRating] = useState();
  const [sort,setSort]=useState('desc');
 


  useEffect(() => {
 const fetchFeedback = async () => {

  try {
  
   
    const params = new URLSearchParams();
    if (rating !== null && rating !== undefined) {
       params.append("rating", rating);
    }

   if (sort !== null && sort !== undefined) {
       params.append("sort", sort);
   }
   const response = await fetch(`http://localhost:5000/feedback?${params.toString()}`);
   //const response = await fetch(`http://localhost:5000/feedback?rating=${rating}&sort=${sort}`);
     if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
     }
    const data = await response.json();
    console.log('data:'+data,3)
    setFeedback(data);
     } catch (err) {
    console.error('Fetch error:', err);
    }
    };

  fetchFeedback();
 }, [rating, sort]); // include sort if you want it to trigger re-fetch


  return (
    <div>
      <h1>Feedback Dashboard</h1>
      <select onChange={(e) => setRating(e.target.value)}>
        <option value="">All Ratings</option>
        <option value="5">5 Stars</option>
        <option value="4">4 Stars</option>
        <option value="3">3 Stars</option>
        <option value="2">2 Stars</option>
        <option value="1">1 Star</option>
      </select> 
      <ul>
        
        {feedback.map((f, i) => (
          <li key={i}>{f.message} - {f.rating} stars - {f.created_at}</li>
        ))}
      </ul>  
    </div>
  );  
}

export default App;
