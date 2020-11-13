import React, {createContext, useState, useEffect} from 'react';

const authkey = 'kwyjhLhydUm6wYKI9ioJVk8NUkj94o9P';
const searchdate = '2020-01-10';


export const ExchangeRateContextValue = {
    data : [],
    date : '2020-11-12',
    setData: () => {},
}

export const ExchangeRateContext = createContext();

export function ExchangeRateContextProvider(props){
    const [data, setData] = useState([]);

    const [date, setDate] = useState('2020-11-12');

    useEffect(()=> {
        fetch(`https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=${authkey}&searchdate=${date}&data=${'AP01'}`)
        .then(response => {
          return response.json()
        })
        .then(responseJSON => {
          console.log('response: ', responseJSON);
          setData(responseJSON);
        });
      }, [date]);

      return (
          <ExchangeRateContext.Provider 
            value = {{
                data,
                date,
                setData,
            }}>
              {props.children}
          </ExchangeRateContext.Provider>
      )
}

export default ExchangeRateContextProvider;