import React ,{useContext,useEffect} from 'react';
import {ExchangeRateContext, } from '../contexts/ExchangeRateContext';
import {Link, } from 'react-router-dom';

function Main(props){
    const exchangeRateContext = useContext(ExchangeRateContext);

    useEffect(() => {
        console.log('exchangeRateContext.data' , exchangeRateContext.data) ;
    }, [exchangeRateContext.data]);

    return (


        <div>
            <div>
                개발중ㅋㅋㅋ
                신기하네
            </div>
            {exchangeRateContext.data.map((currency,cI)=> {
                return (
                    <div key = {cI}>
                        {currency.cur_nm} ({currency.cur_unit}) : {currency.bkpr}
                    </div>
                );
            })}
        </div>
    )

}

export default Main;