import React, {createContext, useState, useEffect} from 'react';

const authkey = 'OEIDkG6msYquVZXRoO4v24mfhCwNPzZ9';
const searchdate = '2020-01-10';


export const ExchangeRateContextValue = {
    data : [],
    setData: () => {},
}

export const ExchangeRateContext = createContext();

export function ExchangeRateContextProvider(props){
    const [data, setData] = useState([]);

    useEffect(()=> {
        fetch(`https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=${authkey}&searchdate=${searchdate}&data=${'AP01'}`)
        .then(response => {
          return response.json()
        })
        .then(responseJSON => {
          console.log('response: ', responseJSON);
          setData(responseJSON);
        });
      }, []);

      return (
          <ExchangeRateContext.Provider 
            value = {{
                data,
            }}>
              {props.children}
          </ExchangeRateContext.Provider>
      )
}

export default ExchangeRateContextProvider;