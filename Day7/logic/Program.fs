namespace logic

open System
open System.Collections.Generic
open System.Linq
open Advent

module Program =
    type bitExpression =
        {
            evaluationFunc: unit -> uint16;
            operands: string array;
        }

    [<EntryPoint>]
    let main argv =
        let lines = Helper.readLines(argv.[0])
        let registers = new Dictionary<string, uint16>()
        let expressions = new Dictionary<string, bitExpression>()

        let operandEvaluatable operand =
            match operand with
                | Regex "([a-zA-Z]+)" [variable] -> registers.ContainsKey variable
                | Regex "([0-9]+)" [_] -> true
                | _ -> raise(InvalidOperationException("Couldn't determine if the operand was evaluatable."))

        let evalOperand operand =
            match operand with
                | Regex "([a-zA-Z]+)" [variable] -> registers.[variable]
                | Regex "([0-9]+)" [number] -> uint16 number
                | _ -> raise(InvalidOperationException("Couldn't determine operand type."))

        let getBitExpression operation =
            let createBitExpression evalFunc operands =
                {
                    evaluationFunc = evalFunc;
                    operands = operands;
                }

            match operation with
                | Regex "^([0-9a-zA-Z]+)$" [operand] ->
                    createBitExpression (fun() -> evalOperand operand) [|operand|]
                | Regex "NOT ([0-9a-zA-Z]+)" [operand] ->
                    createBitExpression (fun() -> ~~~ (evalOperand operand)) [|operand|]
                | Regex "([0-9a-zA-Z]+) AND ([0-9a-zA-Z]+)" [operand1; operand2] ->
                    createBitExpression (fun() -> (evalOperand operand1) &&& (evalOperand operand2)) [|operand1; operand2|]
                | Regex "([0-9a-zA-Z]+) OR ([0-9a-zA-Z]+)" [operand1; operand2] ->
                    createBitExpression (fun() -> (evalOperand operand1) ||| (evalOperand operand2)) [|operand1; operand2|]
                | Regex "([0-9a-zA-Z]+) LSHIFT ([0-9a-zA-Z]+)" [operand1; operand2] ->
                    createBitExpression (fun() -> (evalOperand operand1) <<< (int32 (evalOperand operand2))) [|operand1; operand2|]
                | Regex "([0-9a-zA-Z]+) RSHIFT ([0-9a-zA-Z]+)" [operand1; operand2] ->
                    createBitExpression (fun() -> (evalOperand operand1) >>> (int32 (evalOperand operand2))) [|operand1; operand2|]
                | _ -> raise(InvalidOperationException("Couldn't determine operation type."))

        let buildExpressions expression =
            match expression with
                | Regex "(.*) -> ([a-zA-Z]+)" [operation; register] ->
                    expressions.[register] <- (getBitExpression operation)
                | _ -> raise(InvalidOperationException("Couldn't determine expression type."))

        Seq.iter buildExpressions lines
        while registers.Count <> expressions.Count do
            let evaluatableKeys =
                Seq.filter (fun key -> Seq.forall operandEvaluatable expressions.[key].operands) expressions.Keys
            Seq.iter (fun key -> registers.[key] <- expressions.[key].evaluationFunc()) evaluatableKeys

        registers.Keys
        |> Seq.sort
        |> Seq.iter (fun key -> printfn "%s: %d" key (registers.[key]))
        0
