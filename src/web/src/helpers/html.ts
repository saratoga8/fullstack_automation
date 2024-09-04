type elementId = 'warning' | 'error'

export const setElementHidden = (element: elementId, hidden: boolean) => {
    (document.getElementById(element) as HTMLElement).hidden = hidden
}

