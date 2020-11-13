import React, { useEffect,useState, } from 'react';
import {BrowserRouter} from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import {ExchangeRateContextProvider, } from './contexts/ExchangeRateContext';
import RootRouter from './routers/RootRouter';


function App(){
  return (
    <ExchangeRateContextProvider>
      <BrowserRouter>
        <RootRouter />
      </BrowserRouter>

    </ExchangeRateContextProvider>

  );

}


export default App;


// const authkey = 'OEIDkG6msYquVZXRoO4v24mfhCwNPzZ9';
// const searchdate = '2020-01-10';

// function App() {
//   const [data, setData] = useState([]);

//   useEffect(()=> {
//     fetch(`https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=${authkey}&searchdate=${searchdate}&data=${'AP01'}`)
//     .then(response => {
//       return response.json()
//     })
//     .then(responseJSON => {
//       console.log('response: ', responseJSON);
//       setData(responseJSON);
//     });
//   }, []);
  
//   useEffect(()=> {
//     console.log('data:',data);
//   },[data]);

//   return (
//     <div>
//       {data.map((currency, cI)=> {
//         return (
//           <div key = {cI}>
//             {currency.cur_nm} ({currency.cur_unit}) : {currency.bkpr}

//           </div>
//         );
//       })}
//     </div>
//   );
// }
// export default App;
