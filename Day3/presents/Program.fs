namespace parenthesis

open System
open System.Linq
open Advent

module Program =
    [<EntryPoint>]
    let main argv =
        let input = Helper.readLines(argv.[0]).First()
        let move (moveCharacter:char) (currentLocation:int * int) =
            match moveCharacter with
                | '^' -> (fst currentLocation, snd currentLocation + 1)
                | 'v' -> (fst currentLocation, snd currentLocation - 1)
                | '>' -> (fst currentLocation + 1, snd currentLocation)
                | '<' -> (fst currentLocation - 1, snd currentLocation)
                | c -> raise (InvalidOperationException("Don't know how to deal with a particular move character."))

        let rec deliver index currentLocation (visitedSet : Set<int * int>) =
            let currentChar = input.Chars(index)
            let newLocation = move currentChar currentLocation
            let newSet = visitedSet.Add(newLocation)
            if index < input.Length - 1 then
                deliver (index + 1) newLocation newSet
            else
                newSet

        let locationsVisited = deliver 0 (0, 0) (Set.empty.Add((0, 0)))
            
        printfn "HousesVisited = %d" locationsVisited.Count
        0
